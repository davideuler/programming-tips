
# Create a Job in Java Client


## 1. Maven dependencies

Make sure specify the version of kubernetes-client to 6.4.1, and include vertx httpclient, also the kubernetes-client-api.

```
<dependency>
<groupId>io.fabric8</groupId>
<artifactId>kubernetes-client</artifactId>
<version>6.4.1</version>
<exclusions>
    <exclusion>
        <groupId>io.fabric8</groupId>
        <artifactId>kubernetes-httpclient-okhttp</artifactId>
    </exclusion>
</exclusions>
</dependency>

<dependency>
<groupId>io.fabric8</groupId>
<artifactId>kubernetes-httpclient-vertx</artifactId>
<version>6.4.1</version>
</dependency>

<dependency>
<groupId>io.fabric8</groupId>
<artifactId>kubernetes-client-api</artifactId>
<version>6.4.1</version>
</dependency>


<dependency>
<groupId>org.springframework.cloud</groupId>
<artifactId>spring-cloud-starter-kubernetes-fabric8-all</artifactId>
</dependency>

```

## 2.Create k8s job in kubernetes client. 

```
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

import io.fabric8.kubernetes.api.model.*;
import io.fabric8.kubernetes.api.model.batch.v1.Job;
import io.fabric8.kubernetes.api.model.batch.v1.JobBuilder;
import io.fabric8.kubernetes.client.DefaultKubernetesClient;
import io.fabric8.kubernetes.client.KubernetesClient;
import io.fabric8.kubernetes.client.KubernetesClientException;
```


```
ContainerSpec containerSpec = createSpec(specType);

List<ContainerSpec.Volume> volumes = buildContainerVolume(instanceId);


    public void startJob(ContainerSpec spec, List<ContainerSpec.Volume> volumes, String namespace, String jobName, String imageName, String containerName, String configYamlPath,
                         String command, List<String> args) {
        try (KubernetesClient client = new DefaultKubernetesClient()) {

            String randomUid = UUID.randomUUID().toString();
            ObjectMeta metadata = new ObjectMetaBuilder().withNamespace(namespace).withName(jobName).withUid(randomUid).build();

            // step1. define volume, PV, PVC
            List<PersistentVolume> pvs = createPVs(spec, metadata, volumes, NetUtils.RegionId);

            // create Persistent Volumes
            pvs.stream().peek(pv -> log.info("creating pv: {}", pv.getMetadata().getName())).forEach(pv -> {
                PersistentVolume check = client.persistentVolumes().withName(pv.getMetadata().getName()).get();
                if (check == null || check.getStatus() == null) {
                    client.persistentVolumes().resource(pv).create();
                    log.info("create PV: {}/{}", namespace, pv.getMetadata().getName());
                }
            });

            // // create Persistent Volume Claims
            List<PersistentVolumeClaim> pvcs = volumes.stream().map(v -> createPVC(spec, metadata, namespace, v.getName())).collect(Collectors.toList());
            pvcs.stream().forEach(pvc -> {
                PersistentVolumeClaim check = client.persistentVolumeClaims().inNamespace(namespace).withName(pvc.getMetadata().getName()).get();
                if (check == null || check.getStatus() == null) {
                    client.persistentVolumeClaims().resource(pvc).create();
                    log.info("create PVC: {}/{}", namespace, pvc.getMetadata().getName());
                }
            });

            // Step2. create k8s Volume and Volume Mount
            List<Volume> k8sVolumes = volumes.stream().map(v -> new VolumeBuilder()
                .withName(v.getName()).withNewPersistentVolumeClaim(buildPVCName(metadata, v.getName()), false)
                .build()).collect(Collectors.toList());
            List<VolumeMount> volumeMounts = volumes.stream().map(v ->
                new VolumeMountBuilder().withName(v.getName()).withMountPath(v.getTargetPath()).build()).collect(Collectors.toList());

            List<EnvVar> envVars = new ArrayList<>();
            envVars.add(new EnvVarBuilder().withName("OSS_BUCKET").withValue(spec.getBucketName()).build());
            envVars.add(new EnvVarBuilder().withName("OSS_ENDPOINT").withValue(String.format("oss-%s-internal.aliyuncs.com", regionId)).build());
            JSONObject envs = JSON.parseObject(spec.getEnvs());
            if (envs != null) {
                envs.entrySet().stream().forEach(e -> {
                    envVars.add(new EnvVarBuilder().withName(e.getKey()).withValue(String.valueOf(e.getValue())).build());
                });
            }

            Map<String, Quantity> resources = new HashMap<>();
            resources.put("cpu", new Quantity("" + spec.getResource().getCpu()));
            resources.put("memory", new Quantity(spec.getResource().getMem() + "Gi"));

            if (spec.getResource().getGpu() > 0) {
                resources.put("nvidia.com/gpu", new Quantity(spec.getResource().getGpu() + ""));
            }

            //annotation for aliyun GPU ecs
            Map<String, String> annotations = new HashMap<>();

            if (envs != null && StringUtils.isNotEmpty(envs.getString("ecsSpec"))) {
                annotations.put("k8s.aliyun.com/eci-use-specs", envs.getString("ecsSpec"));
            }

            // 3. Create Job
            Job job = new JobBuilder()
                    .withNewMetadata().addToLabels("app", metadata.getName())
                        .withName(jobName)
                    .endMetadata()
                    .withNewSpec()
                        // time to live for finished/failed jobs, 60min
                        .withTtlSecondsAfterFinished(3600)
                        .withNewTemplate()
                            .withNewMetadata().withAnnotations(annotations).endMetadata()
                            .withNewSpec() //.withVolumes(volumes)
                                .addAllToVolumes(k8sVolumes)
                                .addNewContainer()
                                    .withName(containerName)
                                    .withImage(imageName)
                                    .withCommand(command).withArgs(args)
                                    .withEnv(envVars)
                                    .withNewResources()
                                        .addToRequests(resources).addToLimits(resources)
                                    .endResources()
                                    .addAllToVolumeMounts(volumeMounts)
                                .endContainer()
                                //.withServiceAccountName("my-service-account")
                    .withRestartPolicy("Never")
                    .endSpec()
                    .endTemplate()
                    .endSpec()
                    .build();

            log.info("Creating job:{}", jobName);
            client.batch().jobs().inNamespace(namespace).createOrReplace(job);

            // Step4. Get All pods created by the job, and try to print job's Log:
            PodList podList = client.pods().inNamespace(namespace).withLabel("job-name", job.getMetadata().getName()).list();

            try {
                // Wait for pod to complete
                client.pods().inNamespace(namespace).withName(podList.getItems().get(0).getMetadata().getName())
                    .waitUntilCondition(pod -> pod.getStatus().getPhase().equals("Succeeded"), 1, TimeUnit.MINUTES);
            } catch (KubernetesClientTimeoutException e) {
                log.info("Timeout waiting pod to finish");
            } catch(Exception exec){
                log.warn("Could not get pod info for the job:{}", job.getMetadata().getName(), exec);
            }

            try {
                // Print Job's log
                log.info("Logs from the job:{}", jobName);
                String jobLogs = client.batch().jobs().inNamespace(namespace).withName(jobName).getLog();
                log.info(jobLogs);
            } catch (Exception e) {
                log.warn("Failed to get log for the job:{}", job.getMetadata().getName(), e);
            }
        } catch (KubernetesClientException e) {
            log.error("Error launching job: " + e.getMessage(), e);
        }
    }

```


```
public List<PersistentVolume> createPVs(ContainerSpec spec, ObjectMeta metadata, List<ContainerSpec.Volume> volumes, String regionId) {
        return volumes.stream().map(v -> createPV(spec, metadata, v.getName(), v.getFromPath(), regionId)).collect(
            Collectors.toList());
    }

    public PersistentVolume createPV(ContainerSpec spec, ObjectMeta metadata, String suffix, String ossPath, String regionId) {
        String pvName = buildPVCName(metadata, suffix);
        String amount = spec.getStorage() + "Gi";
        String ossEndpoint = String.format("oss-%s-internal.aliyuncs.com", regionId);
        String[] ts = spec.getAksk().split(":");
        String ak = ts[0], sk = ts[1];

        return new PersistentVolumeBuilder()
            .withNewMetadata()
            .withName(pvName)
            .addToLabels("alicloud-pvname", pvName)
            .addToLabels("app", metadata.getName())
            .withOwnerReferences(buildOwnerReference(metadata))
            .endMetadata()
            .withNewSpec()
            .withAccessModes("ReadWriteMany")
            .addToCapacity("storage", new Quantity(amount))
            .withNewCsi()
            .withDriver("ossplugin.csi.alibabacloud.com")
            .withVolumeAttributes(null)
            .addToVolumeAttributes("bucket", spec.getBucketName())
            .addToVolumeAttributes("otherOpts", "-o allow_other -o nonempty ")
            .addToVolumeAttributes("path", ossPath)
            .addToVolumeAttributes("url", ossEndpoint)
            .addToVolumeAttributes("akId", ak)
            .addToVolumeAttributes("akSecret", sk)
            .withVolumeHandle(pvName)
            .endCsi()
            .withPersistentVolumeReclaimPolicy("Retain")
            .withVolumeMode("Filesystem")
            .withStorageClassName("oss")
            .endSpec()
            .build();
    }

    private String buildPVCName(ObjectMeta metadata, String pvcName) {
        return metadata.getName() + "-" + pvcName;
    }
    public PersistentVolumeClaim createPVC(ContainerSpec spec, ObjectMeta metadata, String namespace, String suffix) {
        String pvName = buildPVCName(metadata, suffix);
        String pvcName = pvName;
        String amount = spec.getStorage() + "Gi";

        return new PersistentVolumeClaimBuilder()
            .withNewMetadata()
            .withNamespace(namespace)
            .withName(pvcName)
            .withOwnerReferences(buildOwnerReference(metadata))
            .endMetadata()
            .withNewSpec()
            .withAccessModes("ReadWriteMany")
            .withNewResources()
            .addToRequests("storage", new Quantity(amount))
            .endResources()
            .withNewSelector()
            .addToMatchLabels("alicloud-pvname", pvName)
            .endSelector()
            .withVolumeName(pvcName)
            .withStorageClassName("oss")
            .endSpec()
            .build();
    }

    private OwnerReference buildOwnerReference(ObjectMeta metadata) {
        return new OwnerReferenceBuilder()
            .withApiVersion(API_VERSION)
            .withController(Boolean.TRUE)
            .withBlockOwnerDeletion(Boolean.TRUE)
            .withKind("object")
            .withName(metadata.getName())
            .withUid(metadata.getUid())
            .build();
    }

static public List<ContainerSpec.Volume> buildContainerVolume(String instanceId) {
        return Arrays.asList(
            new ContainerSpec.Volume("attacheVolume", "/" + instanceId + "/data/", "/app/myapplication/data/")
        );
}

private ContainerSpec createSpec(ResourceSpecType resourceSpecType){
        ContainerSpec spec = new ContainerSpec();

        ResourceSpecType rs = resourceSpecType;

        spec.setReplicas(1);
        
        spec.setImagePullSecret(imagePullSecret);
        spec.setOtsInstanceName(otsInstanceName);
        spec.setBucketName(bucketName);
        spec.setAksk(String.format("%s:%s", accessKey, accessSecret));
        spec.setResource(new ContainerSpec.Resource(rs.cpu, rs.mem, rs.gpu, rs.gpuTag));
        JSONObject envs = new JSONObject();
        
        envs.put("USER_ID", "user_id");
        envs.put("ecsSpec", rs.ecs);
        spec.setEnvs(envs.toString());
        
        spec.setStorage(100);
        return spec;
    }

@Data
public class ContainerSpec implements KubernetesResource {

    String image;
    Integer replicas;
    String imagePullSecret;
    String bucketName;
    
    /** ak:sk; */
    String aksk;
    String otsInstanceName;

    /** json-map */
    String envs;

    //in GB
    Integer storage;

    Resource resource;

    List<Volume> volumes;

    @Data
    @AllArgsConstructor
    public static class Volume {
        String name;

        /** OSS bucket  */
        String fromPath;

        /** target path in container  */
        String targetPath;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class Resource {

        //vcore
        int cpu;

        //Gi
        int mem;

        // gpu count
        int gpu;
    }

}
```

## 3.Test the client

Configure you local ~/.kube/config file, and then can run the code to test.


## 4.Service account 

Configured service account doesn't have access. Service account may have been revoked. jobs.batch is forbidden: User  cannot create resource "jobs" in API group "batch" in the namespace

$ kubectl create clusterrolebinding default-shared-sa-bd --clusterrole=cluster-admin --serviceaccount=mynamespace-test:default-shared-sa

show rolebindings for service account:
$ kubectl get rolebindings,clusterrolebindings --all-namespaces | grep <serviceaccount-name>


## 5.Operators
https://blog.container-solutions.com/cloud-native-java-infrastructure-automation-with-kubernetes-operators

## 6.Listening to events of pod

```
        Set<String> podNames = client.pods().inNamespace(namespace).withLabel("app", workspaceId).resources().map(p -> p.get().getMetadata().getName()).collect(Collectors.toSet());
        
        Watch watch = client.v1().events().inNamespace(namespace).watch(new Watcher<Event>() {
            @Override
            public void eventReceived(Action action, Event event) {
                if (event.getInvolvedObject() == null || false == podNames.contains(event.getInvolvedObject().getName())) {
                    return;
                }
                Deployment deployment = client.apps().deployments().inNamespace(namespace).withName(workspaceId).get();
                if (deployment != null) {
                    DeploymentStatus status = getStatus(deployment.getMetadata(), deployment.getStatus());
                    status.setLastUpdateTime(getEventTime(event));
                    status.setMessage(event.getMessage());
                    log.info("Watched Event action:{} status={}:{}", action, status.getType(), status.getMessage());
                }
            }

            @Override
            public void onClose(WatcherException cause) {

            }
        });

    private String getEventTime(Event event) {
        if (event.getEventTime() != null) {
            return event.getEventTime().getTime();
        }
        if (event.getLastTimestamp() != null) {
            return event.getLastTimestamp();
        }
        if (event.getMetadata().getCreationTimestamp() != null) {
            return event.getMetadata().getCreationTimestamp();
        }
        return event.getLastTimestamp();
    }
```
