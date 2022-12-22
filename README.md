# 图书馆预约脚本

[![My Skills](https://skillicons.dev/icons?i=python,vscode,git)](https://skillicons.dev)

### 禁止任何人使用此项目提供付费的代挂服务

本项目仅供学习交流使用，如作他用所承受的任何直接、间接法律责任一概与作者无关  
如果此项目侵犯了您或者您公司的权益，请立即联系我删除



### 项目说明

- `utils.py` 完成自动预约的py脚本
- `appointment_seat.py` 启动该文件
- `logging.log` 错误信息文件
- `requirements.txt` py依赖库以及版本说明文件

### 使用方法:

1. 先将该项目`clone`到本地

```shell
git clone https://github.com/rinuandengfeng/library
```

2. 安装环境

```shell
pip install -r requirements.txt
```

3. 修改预约信息  
   需要在`utils`中的`LibrarySeat`类中的`choice_seat`中的

```python
data = {
    "SYNCHRONIZER_TOKEN": str(map_token),
    "SYNCHRONIZER_URI": "/map",
    "authid": "-1",
    "start": '1080',  # 预约的开始时间
    "end": '1260',  # 预约的结束时间
    "date": str(tomorrow),
    "seat": '49218',  # 预约的座位号
}
```

的`start`、`end`、`seat`信息进行抓包修改。 其他的信息不需要进行修改

4. 运行
   运行`appointment_seat.py`文件，根据终端提示的信息进行填写自己的信息。

> 注：`username = 'xxx'`中的"xxx"改为自己的学号，将`password ='xxx'`中的"xxx"改为自己的密码（默认身份证后6位，x改为0）

### 其它

该项目目前只支持河南牧业经济学院的图书馆系统。
