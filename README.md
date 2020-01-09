# Recon

自动化护网/SRC致富脚本

## 如何工作

**还没画...**

## 使用方法

**使用ip.txt文件名**

**IP地址段：x.x.x.x-x.x.x.x**
**or**
**CIDR：x.x.x.x/24**

```
echo ip > ip.txt
chmod +x ./recon.sh
./recon.sh ip.txt
```

or

使用有效域名
```
./recon.sh domain.com
```

## 扫描结果

**程序运行结束会生成新的目录，eresults子目录保存的是Eyewitness扫描结果，nresults子目录保存的是nmap相关结果和漏洞检测结果**
```
php -S server:port //程序根目录下开启http服务
```
http://server:port/[random_name]/eresults/report.html
http://server:port/[random_name]/nresults/nmap-bootstrap.html
http://server:port/[random_name]/nresults/vul.txt

http://server:port/[random_name]/nresults/http-title.txt
http://server:port/[random_name]/nresults/product.txt
http://server:port/[random_name]/nresults/service-names.txt


## 注意事项
- 不要在国内限制Masscan的机房使用，腾讯云/阿里云等。
