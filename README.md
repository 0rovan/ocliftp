#ocliftp

Ocliftp is a simple non-interactive FTP client. Upload or download
your files in one command. It can also be useful if you need FTP and
you are not able to use bash.
##Examples
```sh
ocliftp.py -D -r public/root.dir.gpg -l /home/niska/Downloads/dad.gpg ftp.headcrack
ocliftp.py -U -r /uploads/dad.gpg -l Documents/root.dir.gpg -u niska -p s3cr3t.p@55phr4s3 ftp.headcrack
```
