// User registration logic
function signup(user) {
  if (!user.email || !user.password) return false;
  return true;
}
