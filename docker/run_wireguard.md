
## wg-easy: The easiest way to run WireGuard VPN + Web-based Admin UI.

https://github.com/WeeJeWel/wg-easy

```
docker run -d --name=wg-easy \
  -e WG_HOST=xxx.com -e PASSWORD=xyz_xxx \
  -v ~/.wg-easy:/etc/wireguard \
  -p 51820:51820/udp -p 51821:51821/tcp \
  --cap-add=NET_ADMIN --cap-add=SYS_MODULE --sysctl="net.ipv4.conf.all.src_valid_mark=1" \
  --sysctl="net.ipv4.ip_forward=1" --restart unless-stopped \
  weejewel/wg-easy
  ```

## How to Accessing the internet with wireguard (Bypassing wg interface)
https://www.reddit.com/r/WireGuard/comments/g1f6mn/accessing_the_internet_with_wireguard_bypassing/

Im trying to figure out how i can bypass all internet traffic away from the vpn on the client machines.

I think what your looking for is allowed IPs in the client config on your windows machine. Set it to

```
AllowedIps = 10.8.0.1/24
`

That should send that subnet over Wireguard and everything else over the normal connection.

