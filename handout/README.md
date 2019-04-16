## 运行方式， 项目根目录下

* 服务端：
    * node server/src/app.js
* 客户端：
    * python3 client/auth_client.py

### 需要提前安装依赖

* 服务端：
    * Node: 进入server目录， npm install
    * MongoDB: 需要手动添加用户到lab04->users表中， 每个用户保存用户名和用户名username与其密码的SHA256散列值hash1
    * 可以观察app.js中获取用户信息的代码
    ```nodejs
        let db = await MongoClient.connect(db_url, {useNewUrlParser: true})
        let dbo = db.db('lab04');
        obj = await dbo.collection("users").findOne({username: username})
    ```
* 客户端：
    * tkinter
    * pycrypto