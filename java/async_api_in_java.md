
# timeout control of a CompletableFuture for JDK 9 and above

CompletableFuture.supplyAsync(() -> {   Thread.sleep(200); } ).orTimeout(1, TimeUnit.SECONDS);

# apply when any of the CompletableFuture finished: applyToEither



# wait all tasks to be finished: allOf


CompletableFuture<String> cf1 = demoServiceAsyncExecutor.async(service -> service.hello("123"));

CompletableFuture<String> cf2 = demoServiceAsyncExecutor.async(service -> service.hello("456"));

WebClient<Boolean> cf3 = CompletableFuture.supplyAsync(() -> getDb(id), ThreadPoolConfig.ASYNC_TASK_EXECUTOR);

return CompletableFuture.allOf(cf1, cf2, cf3)
        .thenApply(r -> cf1.join() + cf2.join() + dbFuture.join()).join();
