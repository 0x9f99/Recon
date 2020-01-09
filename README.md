# Recon

自动化护网/SRC致富脚本

## 如何工作

图1

## 使用方法

使用ip.txt文件名
IP地址段：x.x.x.x-x.x.x.x
or
CIDR：x.x.x.x/24

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

## 注意事项
- 不要在国内限制Masscan的机房使用，腾讯云/阿里云等。
