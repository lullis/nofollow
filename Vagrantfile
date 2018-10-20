# -*- mode: ruby -*-
# vi: set ft=ruby :
require 'yaml'

BOX_USERNAME = 'vagrant'.freeze
VAGRANT_API_VERSION = '2'.freeze

BOX = {
  'name' => ENV.fetch('NOFOLLOW_VAGRANT_BOX_NAME', 'nofollow-dev'),
  'ip' => ENV.fetch('NOFOLLOW_VAGRANT_BOX_IP', '192.168.23.15'),
  'memory' => ENV.fetch('NOFOLLOW_VAGRANT_BOX_MEMORY', 4096),
  'cpus' => ENV.fetch('NOFOLLOW_VAGRANT_BOX_CPUS', 2)
}.freeze

ANSIBLE = {
  'config_file' => ENV.fetch(
    'NOFOLLOW_ANSIBLE_CONFIG_FILE', 'ansible/ansible.cfg'
  ),
  'playbook' => ENV.fetch(
    'NOFOLLOW_ANSIBLE_PLAYBOOK_NAME', 'ansible/vagrant.yml'
  ),
  'galaxy_roles_path' => ENV.fetch(
    'NOFOLLOW_ANSIBLE_GALAXY_ROLES_PATH', '/etc/ansible/roles'
  )
}.freeze

Vagrant.configure(VAGRANT_API_VERSION) do |config|
  # required to clone gits
  config.ssh.forward_agent = true

  config.vm.box = 'ubuntu/bionic64'
  config.vm.box_check_update = false

  # Setup ansible
  config.vm.provision 'ansible' do |ansible|
    ansible.compatibility_mode = '2.0'
    ansible.config_file = ANSIBLE['config_file']
    ansible.playbook =  ANSIBLE['playbook']
    ansible.extra_vars = Hash['public_ip' => BOX['ip']]
    ansible.galaxy_roles_path = ANSIBLE['galaxy_roles_path']
  end

  config.vm.define BOX['name'], primary: true do |default|
    default.vm.hostname = "#{BOX['name']}.local"
    default.vm.network :private_network, ip: BOX['ip']
    default.vm.network 'forwarded_port', guest: 8000, host: 8000
    default.vm.synced_folder '.', '/vagrant', disabled: true
    default.vm.synced_folder '.', "/home/#{BOX_USERNAME}/code"

    default.vm.provider :virtualbox do |virtualbox|
      virtualbox.customize ['modifyvm', :id, '--name', BOX['name']]
      virtualbox.customize ['modifyvm', :id, '--memory', BOX['memory']]
      virtualbox.customize ['modifyvm', :id, '--cpus', BOX['cpus']]
    end
    # Fixing locale issue
    default.vm.provision :shell, :inline => <<-EOT
      echo 'LC_ALL="en_US.UTF-8"'  >  /etc/default/locale
    EOT
  end
end
