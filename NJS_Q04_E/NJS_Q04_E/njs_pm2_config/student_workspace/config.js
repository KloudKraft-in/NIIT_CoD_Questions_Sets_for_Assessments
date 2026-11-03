module.exports = {
  apps : [{
    name: 'node-service',
    script: 'app.js',
    // TODO: Configure execution mode to 'cluster', instances to 2, and max_memory_restart to '150M'
    error_file: 'logs/error.log',
    out_file: 'logs/out.log'
  }]
};
