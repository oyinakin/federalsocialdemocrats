function sortTable(n, obj) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = ((obj.parentNode).parentNode).parentNode;
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {

    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("td")[n];
      y = rows[i + 1].getElementsByTagName("td")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {

          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}


$(document).ready(function() {
  $("#myInput").on("keyup", function() {
  var value = $(this).val().toLowerCase();
  $("#myTbody2 tr").filter(function() {
  $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
});
});
 $("#paymentsearch").on("keyup", function() {
 var value = $(this).val().toLowerCase();
 $("#myTbody3 tr").filter(function() {
 $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
});
});
$("#myreferral").on("keyup", function() {
var value = $(this).val().toLowerCase();
$("#myTbody4 tr").filter(function() {
$(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
});
});
  $("#overview").show();
  $('.nav-btn').on('click', function(event) {
    event.preventDefault();
    /* Act on the event */
    $('.sidebar').slideToggle('slow');
    $(".hidelogo").hide();
    window.onresize = function(){
      if ($(window).width() >= 768) {
        $('.sidebar').show();
        $(".hidelogo").show();
      } else {
        $('.sidebar').hide();
        $(".hidelogo").hide();
      }
    };
  });
});
$(document).ready(function(){
 $('.trigger').click(function() {
    $('.modal-wrapper').toggleClass('open');
    if($('.modal-wrapper.open')){
       $(".filterlinks.active").click()
    }
     return false;
 });
 $('.trigger4').click(function() {
    $('.profile-wrapper').toggleClass('open');
    return false;
 });
 $('.trigger2').click(function() {
    $('.sms-wrapper').toggleClass('open');
     return false;
 });
 $('.trigger3').click(function() {
    $('.email-wrapper').toggleClass('open');
     return false;
 });
 $('.trigger8').click(function() {
    $('.edit-post-wrapper').toggleClass('open');
     return false;
 });
 $('.triggerpost').click(function() {
    $('.post-wrapper').toggleClass('open');
     return false;
 });
});

$(function(){

  $.each($(".print-tab .print-tab-menu > li"), function(index, value){
    var menu = $(value).data('tab-menu');
    var tabID = $(value).parent().parent().data('tab-id');
    var hash = window.location.hash.split("#").join('');

    if(hash.length > 0){

      if(menu == hash){
        $('.print-tab[data-tab-id="' + tabID + '"] .print-tab-menu > li[data-tab-menu="' + menu + '"]').addClass('active');
        $('.print-tab[data-tab-id="' + tabID + '"] .print-tab-content > div[data-tab-content="' + menu + '"]').addClass('view');
      }

    }else{
      $('.print-tab[data-tab-id="' + tabID + '"] .print-tab-menu > li:eq(0)').addClass('active');
      $('.print-tab[data-tab-id="' + tabID + '"] .print-tab-content > div:eq(0)').addClass('view');
    }
  });



  $(".print-tab .print-tab-menu > li").click(function(event){
    var $this = $(this),
      $data = $this.data('tab-menu'),
      $tabID = $this.parent().parent().data('tab-id');
    if(!$(this).hasClass("active")){

      window.location.hash = $data;

      $('.print-tab[data-tab-id="' + $tabID + '"] .print-tab-menu > li').removeClass('active');
      $(this).addClass('active');

      $('.print-tab[data-tab-id="' + $tabID + '"] .print-tab-content > div.view').removeClass('view');
      $('.print-tab[data-tab-id="' + $tabID + '"] .print-tab-content > div[data-tab-content="' + $data + '"]').addClass('view');
    }
  });
});
