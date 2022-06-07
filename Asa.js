function formCheck() {
  var name = document.getElementById("name").value;
  var age = document.getElementById("age").value;
  var phone = document.getElementById("phone").value;
  var address = document.getElementById("address").value;
  var userid = document.getElementById("userid").value;
  age = Number(age);
  
  if (age <18) {
    alert("你未成年！")
  };
  
  if (name==""){
    alert("你尚未填寫姓名")
  };
  
  if (phone==""){
    alert("你尚未填寫電話")
  };
  
  if (address==""){
    alert("你尚未填寫地址")
  };
  
  if (userid==""){
    alert("你尚未填身分證字號")
  };
  
 return false
}
