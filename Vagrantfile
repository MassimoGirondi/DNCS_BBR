# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box_check_update = false
  config.vm.provider "virtualbox" do |vb|
    # Change the management network address to not give problems to routing
    # Usually it's 10.0.0.0/8
    vb.customize ["modifyvm", :id, "--natnet1", "192.168.100/24"]
    vb.memory = 2048
    vb.cpus = 2
  end
  config.vm.define "mininet-1" do |mininet1|
    mininet1.vm.box = "generic/debian9"
    mininet1.vm.hostname = "mininet-1"
    #mininet1.vm.provision "file", source: ".",  destination: "~/DNCS_BBR"
    config.vm.synced_folder "./", "/home/vagrant/DNCS_BBR"
  end
end
