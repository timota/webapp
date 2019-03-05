# Build env

Vagrant.configure("2") do |config|
  # Base VM OS configuration.
  config.vm.box = "debian/stretch64"
  
  # lets use our key
  config.ssh.insert_key = false
  config.ssh.forward_agent = true
  config.ssh.private_key_path = ["~/.ssh/id_rsa", "~/.vagrant.d/insecure_private_key"]
  config.vm.provision "file", source: "~/.ssh/id_rsa.pub", destination: "~/.ssh/authorized_keys"
  #config.vm.provision "shell", inline: <

  # disable sync dir
  config.vm.synced_folder '.', '/vagrant', disabled: true

  # General VirtualBox VM configuration.
  config.vm.provider :virtualbox do |generic|
    generic.memory = 512
    generic.cpus = 1
    generic.linked_clone = true
    generic.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    generic.customize ["modifyvm", :id, "--ioapic", "on"]
  end

  # ans-db
  config.vm.define "db" do |db|
    db.vm.hostname = "ans-db"
    db.vm.network :private_network, ip: "192.168.32.2"
  end

  # ans-app-01
  config.vm.define "app1" do |app1|
    app1.vm.hostname = "ans-app-01"
    app1.vm.network :private_network, ip: "192.168.32.3"
    
    app1.vm.provider :virtualbox do |generic|
      generic.customize ["modifyvm", :id, "--memory", 256]
    end
  end

  # ans-lb
  config.vm.define "lb" do |lb|
    lb.vm.hostname = "ans-lb"
    lb.vm.network :private_network, ip: "192.168.32.4"
    
    lb.vm.provider :virtualbox do |generic|
      generic.customize ["modifyvm", :id, "--memory", 256]
    end
    
    # Run Ansible provisioner once for all VMs at the end.
    lb.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbooks/configure.yml"
      ansible.inventory_path = "playbooks/inventory"
      ansible.limit = "all"
      ansible.host_key_checking = false
      ansible.extra_vars = {
        ansible_ssh_user: 'vagrant',
        ansible_ssh_private_key_file: "~/.vagrant.d/insecure_private_key"
      }
    end

  end
end
    
