function openWhatsApp(){
  // Opens WhatsApp with a predefined message (uses number from settings via template context if available)
  var phone = window.EVERCARE && window.EVERCARE.whatsapp ? window.EVERCARE.whatsapp : '+254723900873';
  var msg = encodeURIComponent('Hello Evercare Garage, I would like to enquire about a service.');
  var url = 'https://wa.me/' + phone.replace(/\D/g,'') + '?text=' + msg;
  window.open(url, '_blank');
}

// Simple counter animation
document.addEventListener('DOMContentLoaded', function(){
  var counters = document.querySelectorAll('.counter');
  counters.forEach(function(c){
    // leave as static numbers (from template) for simplicity; could animate if data attributes set
  });
});
