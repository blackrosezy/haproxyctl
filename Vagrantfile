$script = <<SCRIPT
    if ! type fig > /dev/null 2>&1
    then
        curl -o /usr/local/bin/fig -L https://www.dropbox.com/s/64yi3c1px4l9rq9/docker-compose-Linux-x86_64?dl=1
        chmod +x /usr/local/bin/fig
    fi
    
    if ! type docb > /dev/null 2>&1
    then
        curl -o /usr/local/bin/docb -L https://raw.githubusercontent.com/blackrosezy/docker-essential-tools/master/docb && chmod +x /usr/local/bin/docb
        curl -o /usr/local/bin/docc -L https://raw.githubusercontent.com/blackrosezy/docker-essential-tools/master/docc && chmod +x /usr/local/bin/docc
        curl -o /usr/local/bin/doci -L https://raw.githubusercontent.com/blackrosezy/docker-essential-tools/master/doci && chmod +x /usr/local/bin/doci
        curl -o /usr/local/bin/n -L https://raw.githubusercontent.com/blackrosezy/docker-essential-tools/master/n && chmod +x /usr/local/bin/n
    fi
    
    apt-get install python-pip -y
    
    mkdir /packaging && cp -r /vagrant/* /packaging
    cd /packaging && python setup.py sdist
    
    # nginx
    cd /vagrant/vagrant-assets/nginx
    fig build --no-cache && fig up -d
    
    # haproxy
    cd /vagrant/vagrant-assets/haproxy
    fig build --no-cache && fig up -d

    # cleanup
    docb
SCRIPT

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  
  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 1
    
    # speedup network
    v.customize ["modifyvm", :id, "--nictype1", "virtio" ]
    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end
  
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 9000, host: 9000
  config.vm.network "forwarded_port", guest: 3306, host: 3307
  
  config.ssh.insert_key = false
  config.ssh.forward_agent = true

  # install docker
  config.vm.provision "docker"
  
  # run custom script
  config.vm.provision "shell", inline: $script
end
