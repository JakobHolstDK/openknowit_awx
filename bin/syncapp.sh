ssh dashapp01fl "sudo  chown -R rks221:dash /opt/dash/app"
rsync -avc app/* dashapp01fl:/opt/dash/app
signssh
rsync -avc app/* openstack03:/opt/dash/app
ssh dashapp01fl "sudo  chown -R dash:dash /opt/dash/app"
