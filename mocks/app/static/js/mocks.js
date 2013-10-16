
/*
    Links
*/
$('.login-link').click(
  function() {
    window.location.href = "/login";
  }.bind(this)
);
$('.register-link').click(
  function() {
    window.location.href = "/register";
  }.bind(this)
);
$('.logout-link').click(
  function() {
    window.location.href = "/logout";
  }.bind(this)
);

$('.home-link').click(
  function() {
    window.location.href = "/home";
  }.bind(this)
);
$('.schedule-link').click(
  function() {
    window.location.href = "/schedule";
  }.bind(this)
);
$('.createslot-link').click(
  function() {
    window.location.href = "/createslot";
  }.bind(this)
);
$('.profile-link').click(
  function() {
    window.location.href = "/profile";
  }.bind(this)
);

/*
  Mockitem button
 */
$('.moreinfo-btn').click( function() {
  window.location.href = this.value;
});