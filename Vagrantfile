$script = <<SCRIPT
    if ! type fig > /dev/null 2>&1
    then
        curl -o /usr/local/bin/fig -L https://github.com/docker/compose/releases/download/1.5.1/docker-compose-Linux-x86_64
        chmod +x /usr/local/bin/fig
    fi
    
    if ! type docb > /dev/null 2>&1
    then
        curl -o /usr/local/bin/docb -L https://raw.githubusercontent.com/blackrosezy/docker-essential-tools/master/docb && chmod +x /usr/local/bin/docb
        curl -o /usr/local/bin/docc -L https://raw.githubusercontent.com/blackrosezy/docker-essential-tools/master/docc && chmod +x /usr/local/bin/docc
        curl -o /usr/local/bin/doci -L https://raw.githubusercontent.com/blackrosezy/docker-essential-tools/master/doci && chmod +x /usr/local/bin/doci
        curl -o /usr/local/bin/n -L https://raw.githubusercontent.com/blackrosezy/docker-essential-tools/master/n && chmod +x /usr/local/bin/n
    fi
    
    if ! type jq > /dev/null 2>&1
    then
        curl -o /usr/local/bin/jq -L https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64
        chmod +x /usr/local/bin/jq
    fi
    
    docker pull nginx:latest
    docker stop web1 && docker rm -f web1
    cd /vagrant/vagrant-assets/nginx && docker build -t my-nginx .
    docker run -d --restart=always --name web1 my-nginx
    
    docker pull haproxy:latest
    docker stop haproxy1 && docker rm -f haproxy1
    cd /vagrant/vagrant-assets/haproxy && docker build -t my-haproxy .
    docker run -d -p "80:80" --restart=always --name haproxy1 my-haproxy
    
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
  
  config.vm.network "forwarded_port", guest: 80, host: 80
  
  config.ssh.insert_key = false
  config.ssh.forward_agent = true

  # install docker
  config.vm.provision "docker"
  
  # run custom script
  config.vm.provision "shell", inline: $script
end