desc "This task is called by the Heroku scheduler add-on"
task :update_data => :environment do
  puts "Daily update of data..."
  controller.controller.controllerObject.updateArticleData
  puts "done."
end