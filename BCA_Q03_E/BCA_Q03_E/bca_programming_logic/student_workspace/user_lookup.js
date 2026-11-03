// User Lookup Service
function getUserEmail(user) {
  return user.profile.email;
}

module.exports = { getUserEmail };
