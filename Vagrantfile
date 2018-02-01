VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "fedora/27-cloud-base"
    config.vm.box_version = "20171105"

    config.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.customize ["modifyvm", :id, "--cpus", "2"]
    end

    config.vm.provision "shell", path: "provision.sh"
end
