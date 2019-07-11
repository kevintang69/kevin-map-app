$(document).ready(
    function(){
        $(".toggleButton").on('click', 
            function(){
                // let filename = $(this).parent().attr('section_name')
                let filename = this.parentElement.getAttribute("section_name")
                if ( this.innerHTML == 'Show Map'  ){
                    this.innerHTML = 'Hide Map'
                    document.getElementById(filename +"_map").src = '/static/'+filename
                }
                else if (this.innerHTML == 'Hide Map'){
                    this.innerHTML = 'Show Map'
                    document.getElementById(filename +"_map").src = 'static/stock.html'
                }
        });
        
        
        $(".removeButton").on('click',
            function(){
                let filename = this.parentElement.getAttribute("section_name")
                let confirmation = confirm("Are you sure you want to delete " + this.parentElement.getAttribute("section_name") + "?")
                if (confirmation){
                    let req = $.post("update" , {action : 'delete', filename:this.parentElement.getAttribute("section_name"),idnum:this.parentElement.getAttribute("section_id") },
                            function(data){
                                let result = data.result
                                if (result == 'good'){
                                    
                                    

                                    let total = parseInt( document.getElementById('total_count').innerHTML)
                                    let removed = parseInt( document.getElementById(filename+'_section').getAttribute('current_num'))
                                    let e = document.getElementById(filename+"_section")
                                    e.parentNode.removeChild(e)
                                    for ( x = removed+1 ; x<=total ; x++  ){
                                        let new_x = x-1
 
                                        document.getElementById(x.toString()+"_count"  ).innerHTML = new_x.toString()
                                        document.getElementById(x.toString()+"_count"  ).parentElement.setAttribute('current_num',  new_x.toString() )

                                        document.getElementById(x.toString()+"_count"  ).id = new_x.toString() + "_count"
                                    }
                                    let new_total = total -1 
                                    document.getElementById('total_count').innerHTML = new_total.toString()
                                    alert("Item was successfully deleted")
                                }
                                else{
                                    alert("Item failed to delete")
                                    }
                            })
                }
            });


        $(".makeChangesButton").on('click',
            function(){
                this.style.display = 'none'
                document.getElementById(this.parentElement.getAttribute("section_name") +"_makeChangesKit").style.display = 'block'
            }
        );


        $(".cancelButton").click(
            function(){
                let filename = this.parentElement.parentElement.getAttribute("section_name")
                document.getElementById(filename+"_makeChangesButton").style.display = 'block'
                this.parentElement.style.display = 'none'
            }
        );


        $(".submitChangesButton").click(
            function(){
                let filename = this.parentElement.parentElement.getAttribute("section_name")
                let idnum = this.parentElement.parentElement.getAttribute("section_id")
                document.getElementById(filename+"_makeChangesButton").style.display = 'block'
                this.parentElement.style.display = 'none'
                
                let new_coord = document.getElementById(filename+"_changeInput").value
                let req = $.post('/update' , {filename:filename,idnum:idnum,new_coord:new_coord ,action:"change"} ,
                        function(data){
                            if (data.result == 'good'){
                                updateIDs(filename, data.newName)
                            }
                            else{
                                alert("Change unsuccessful or input coordinates same as old ones")
                            }
                        } )
            }
        )


    })
 


function updateIDs(oldName, newName ){
    document.getElementById(oldName+"_section").setAttribute("section_name", newName)
    document.getElementById(oldName+"_paragraph").innerHTML = newName

    if (document.getElementById(oldName + "_map").src != 'static/stock.html'  ){
        document.getElementById(oldName + "_map").src = "static/"+newName
    }

    let suffix_list = [ "section","count","paragraph","map","makeChangesButton","makeChangesKit","changeInput"]
    suffix_list.forEach(function(suffix){
        console.log(newName + "_"+suffix)
        document.getElementById(oldName + "_" +suffix ).id = newName + "_"+suffix
    })
    
}