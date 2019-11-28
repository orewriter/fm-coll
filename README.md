# fm-coll

Berikut adalah composer untuk pembuatan container yang dibutuhkan untuk development FM-coll

untuk dapat berjalan server/PC harus terinstall Berikut

OS minimal turunan RHEL 7/Debian 9 dan terinstall docker-ce dan docker-compose.


untuk petunjuk installasi bisa menuju ke link Berikut

https://docs.docker.com/install/linux/docker-ce/centos/
https://docs.docker.com/install/linux/docker-ce/debian/


setelah terinstall silahkan clone/download git init


didalam docker-compose.yml terdapat comment sebagai petunjuk deploy applikasi

untuk menjalankan silahkan masuk ke directory yang sudah di clone/download lalu ketikan perintah

docker-compose up -d --force-recreate
