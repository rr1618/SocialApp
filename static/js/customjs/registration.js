
var arr=[true,true,true,true,true,true]
function fcheck() {
    if ($("#fname").val().length < 3)
    {
           $("#checkfname").html("Please Enter First Name").show();
        arr[0]=false;
    }

    else
    {
        $("#checkfname").hide();
    arr[0]=true;
    }
}
function lcheck() {
    if ($("#lname").val().length < 3)
    {
        $("#checklname").html("Please Enter last name").show();
    arr[1]=false;
    }
    else
    {
        $("#checklname").hide();
    arr[1]=true;
    }
}
function ucheck() {
        $.ajax({
            data: {
                username: $('#u_name').val(),
            },
            type: "POST",
            url: "/register",
        })
            .done(function (data) {
                if(data.error){
                    $("#checkuname").removeClass().addClass('text-danger').html('Username not available').show()
                    arr[2]=false;
                }
                else {
                    $("#checkuname").removeClass().addClass('text-success').html('available').show()
                    arr[2]=true;
                }
            })
}
function passcheck() {
    cpasscheck()
    if($("#npass").val().length<3)
    {
        console.log($("#npass").val().length)
           $("#checkpass").html("Password must be more than three characters").show()
    }

    else
        $("#checkpass").hide()
}
function cpasscheck() {
        if ($("#npass").val()===$("#cpass").val())
        {
            $("#checkcpass").removeClass('text-danger').addClass('text-success').html("Password Matched").show();
        arr[3]=true;
        }
    else
        {
            $("#checkcpass").removeClass('text-success').addClass("text-danger").html("Password Don't Match").show();
    arr[3]=false;
        }
}
function phonecheck() {
    if ($("#phone").val().length < 3)
    {
        $("#checkphone").html("Wrong Phone Number").show();
    arr[4]=false;
    }
    else
    {
        $("#checkphone").hide();
    arr[4]=true;
    }
}
function emailcheck() {
    if($("#email").val().length<3)
    {
        $("#checkemail").html("email must have more than 3 characters").show();
    arr[5]=false;
    }
    else

    {
        $("#checkemail").hide();
    arr[5]=true;
    }
}
function submitcheck() {
    for(i=0;i<arr.length;i++)
    {
        if (arr[i] == false) {
            return false;
        }
    }
    alert("user Registered , Now login")
    return true
    }
