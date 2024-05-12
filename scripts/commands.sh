scp -r root@hetzner:/root/workplace/Reader/ReaderApi/sqlite.db /Volumes/workplace/Reader/ReaderApi/api/sqlite.db

scp -r /Volumes/workplace/Reader/ReaderApi/api/sqlite.db root@hetzner:/root/workplace/Reader/ReaderApi/sqlite.db
scp -r ~/cookies.txt root@hetzner:~/cookies.txt

ln -sf /Volumes/workplace/Reader/ReaderApi/sqlite.db /Volumes/workplace/Reader/ReaderApi/api/sqlite.db
