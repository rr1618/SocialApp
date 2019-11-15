
function edit(){
        $(".form-group").slideToggle();
    }
function delet(sno) {
    $.ajax({
        data: {
                input2: sno,
            },
            type:"POST",
            url: "/dashboard/delete",
        })
            .done(function (data) {
                if(data.msg=="post deleted"){
                    $(location).attr('href','/dashboard/1');
                }else
                {
                    alert("something went wrong");
                }

            })
    }
    function onedit(sno) {
        $("#sa"+sno).show();
        $("#ed"+sno).hide();
        $.ajax({
            data: {
                input3: sno,
                input4: false,
            },
            type:"POST",
            url: "/dashboard/edit",
        })
            .done(function (data) {
                $("."+sno).replaceWith("<input id=\"edit_title\" class=\"form-control\">");
                $("#edit_title").val(data.post_title)
                $("#po"+sno).replaceWith("<textarea name=\"post\" id=\"edit_post\" class=\"form-control\" placeholder=\"POST\" style=\"width: 100%; height: 150px;\"></textarea>");
                $("#edit_post").val(data.post)


            })

    }

        function saveChange(sno) {
           $.ajax({
            data: {
                input3: sno,
                input4: true,
                post_title: $("#edit_title").val(),
                post: $("#edit_post").val()
            },

            type:"POST",
            url: "/dashboard/edit",
        })
               .done(function (data) {
                    if(data.msg){
                        $(location).attr('href','/dashboard/1');
                    }else
                    {
                        alert("something went wrong");
                    }
               })
        }