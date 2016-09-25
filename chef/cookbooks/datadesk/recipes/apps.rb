# Create the apps directory where everything will go
directory "/apps/" do
    owner node[:apps_user]
    group node[:apps_group]
    mode 0775
end

# Loop through all the apps we want to configure
node[:apps].each do |app|
    
    # Make the directory for the app
    virtualenv "/apps/#{app[:name]}" do
        owner node[:apps_user]
        group node[:apps_group]
        mode 0775
    end
    
    # Make the directory for the repo
    directory "/apps/#{app[:name]}/repo" do
        owner node[:apps_user]
        group node[:apps_group]
        mode 0775
    end
    
    # Pull the git repo
    git "/apps/#{app[:name]}/repo"  do
      repository app[:repo]
      reference "HEAD"
      revision app[:branch]
      user node[:apps_user]
      group node[:apps_group]
      action :sync
    end
    
    # Install the virtualenv requirements
    script "Install Requirements" do
      interpreter "bash"
      user node[:apps_user]
      group node[:apps_group]
      code "/apps/#{app[:name]}/bin/pip install -r /apps/#{app[:name]}/repo/requirements.txt --no-cache-dir"
    end

    # Create the database user
    script "Create database user" do
      interpreter "bash"
      user "postgres"
      code <<-EOH
         psql -c "CREATE USER #{app[:db_user]} WITH INHERIT SUPERUSER CREATEDB PASSWORD '#{app[:db_password]}'";
      EOH
      ignore_failure true
    end

    # Create the database
    script "Create database" do
      interpreter "bash"
      user "postgres"
      code <<-EOH
        createdb #{app[:db_name]} -E UTF8 -O #{app[:db_user]}
      EOH
      ignore_failure true
    end

    # Run any management commands
    app[:management].each do |command|
      script "Running #{command}" do
        interpreter "bash"
        user node[:apps_user]
        code <<-EOH
          cd /apps/#{app[:name]} && . bin/activate && cd repo && /apps/#{app[:name]}/bin/python /apps/#{app[:name]}/repo/manage.py #{command}
        EOH
      end
    end

end
