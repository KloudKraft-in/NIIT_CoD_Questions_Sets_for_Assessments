function generateReport(user) {
  // Missing safe fallbacks. Reference user.profile.email.
  return "User email is: " + user.profile.email;
}
module.exports = { generateReport };
