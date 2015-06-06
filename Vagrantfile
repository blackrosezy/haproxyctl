Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  
  config.vm.provider "virtualbox" do |v|
    v.memory = 512
    v.cpus = 1
  end
  
  config.vm.network "forwarded_port", guest: 80, host: 80
  
  config.ssh.insert_key = false
  config.ssh.forward_agent = true

  config.vm.provision "docker"
  $script = <<SCRIPT
    if ! type fig > /dev/null 2>&1
    then
        curl -o /usr/local/bin/fig -L https://github.com/docker/compose/releases/download/1.3.0rc1/docker-compose-Linux-x86_64
        chmod +x /usr/local/bin/fig
    fi
    
    if ! type docb > /dev/null 2>&1
    then
        curl -o /usr/local/bin/docb -L https://dl.dropboxusercontent.com/u/2375856/docb && chmod +x /usr/local/bin/docb
        curl -o /usr/local/bin/docc -L https://dl.dropboxusercontent.com/u/2375856/docc && chmod +x /usr/local/bin/docc
        curl -o /usr/local/bin/doci -L https://dl.dropboxusercontent.com/u/2375856/doci && chmod +x /usr/local/bin/doci
        curl -o /usr/local/bin/n -L https://dl.dropboxusercontent.com/u/2375856/n && chmod +x /usr/local/bin/n
    fi
    
    if ! type jq > /dev/null 2>&1
    then
        curl -o /usr/local/bin/jq -L https://github.com/stedolan/jq/releases/download/jq-1.5rc1/jq-linux-x86_64-static
        chmod +x /usr/local/bin/jq
    fi
    
    docker stop web1 && docker rm web1
    docker run -d --restart=always --name web1 nginx
    
    docker stop haproxy1 && docker rm haproxy1
    cd /vagrant/vagrant-assets && docker build -t my-haproxy .
    docker run -d -p "80:80" --restart=always --name haproxy1 my-haproxy
SCRIPT
  config.vm.provision "shell", inline: $script
end
