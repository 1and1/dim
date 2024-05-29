ndcli
=====

This is ndcli, the CLI client for DIM.

Linux (.deb, .rpm)
------------------

Packages are available on [github](https://github.com/1and1/dim).


Installation in venv
--------------------
Thanks to almueller for providing this.

Create virtualenv
```
virtualenv -p python3 $HOME/ndcli
```

Download
```
curl https://github.com/1and1/dim/releases/download/ndcli-5.0.2/ndcli-src-5.0.2.tar.gz -o ndcli-src-5.0.2.tar.gz
curl https://github.com/1and1/dim/releases/download/dimclient-1.0.1/dimclient-src-1.0.1.tar.gz -o dimclient-src-1.0.1.tar.gz
```

Extract
```
tar xcf dimclient-src-1.0.1.tar.gz
tar xcf ndcli-src-5.0.2.tar.gz
```

Install
```
ndcli/bin/pip3 install dnspython
ndcli/bin/pip3 install dimclient-1.0.1/
ndcli/bin/pip3 install ndcli-5.0.2
```

Add bash completion
```
echo "complete -C ndcli ndcli" >> .bash_profile
```

Cleanup
```
rm -rf dimclient* && rm -rf ndcli-5.0.2/ && rm -rf dimclient-src-1.0.1.tar.gz && rm -rf ndcli-src-5.0.2.tar.gz
```

Add to path
```
echo "export PATH=\""\$PATH:$HOME/ndcli/bin"\"" >> .bash_profile
```

Configure (ENSURE to set username to your InsideNET/IonosCore Username)
```
cat > ~/.ndclirc << EOF
server=https://dim.svc.1u1.it/dim
username=$USER
layer3domain=default
EOF
```

1st login
```
ndcli login
```

