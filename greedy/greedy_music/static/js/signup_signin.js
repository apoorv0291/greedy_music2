
   $(document).ready(function(){

                    //To be copied
                 console.log("in signup_signin.JS")
                 $('#sign_in_btn').click(function(e){
                    e.preventDefault();
                    console.log("sign_in_btn_clicked")
                    form_data = $('#signin_form').serializeArray()
                    console.log(form_data)
                    url = "/greedymusic/login/"
                    $.ajax({
                               url : url,
                               type : "POST",
                               data : form_data,
                               dataType : "json",
                               success:function(res_data){
                                        console.log(res_data);
                                        var success = res_data['success'];
                                        var message = res_data['message'];
                                        console.log("success: " + success);
                                        console.log("message: " + message);
                                        if(success)
                                        {
                                             console.log("In success == True \n");
                                             alert("successfully loggedin")
                                             //$('#close_btn').trigger( "click" );
                                             window.location.replace("/greedymusic/tracks/")



                                        }
                                        else
                                        {
                                             console.log("In success == false \n");





                                        }

                                     }
                    });


                 })
                //to be copied
                $('#sign_up_btn').click(function(e){
                    e.preventDefault();
                    console.log("sign_up_btn_clicked")
                    form_data = $('#signup_form').serializeArray()
                    console.log(form_data)
                    url = "/greedymusic/register/"
                    $.ajax({
                               url : url,
                               type : "POST",
                               data : form_data,
                               dataType : "json",
                               success:function(res_data){
                                        console.log(res_data);
                                        var success = res_data['success'];
                                        var message = res_data['message'];
                                        console.log("success: " + success);
                                        console.log("message: " + message);
                                        if(success)
                                        {
                                             console.log("In success == True \n");
                                             alert("Successfully registered.")
                                              //$('#close_btn').trigger( "click" );
                                              window.location.replace("/greedymusic/genres/")



                                        }
                                        else
                                        {
                                             console.log("In success == false \n");
                                             var updateErrorMsg = savedTaskForm + " #update-prtcptn-error-msg";



                                        }

                                     }
                    });


                })
   });
