function fn1(x,y,z, b){
    // document.getElementById(z).src = x ;
    // document.getElementById(y).innerHTML = a;
    // document.getElementById(y).onclick = 'fn1( c,y,z, b,a, x    )'  ;

    if ( document.getElementById(y).innerHTML == 'hide' ){
        document.getElementById(y).innerHTML = 'show';
         document.getElementById(z).src = x ;
    }
    else{
        document.getElementById(y).innerHTML = 'hide';
         document.getElementById(z).src = b ;
    }



}



function fn2(x){
    let r = confirm("Are you sure you want to delete?")
    if (r){
        document.getElementById(x+'block').innerHTML = '';
        let idnum = document.getElementById(x+'block').getAttribute('idnum')
        $.post('update', {idnum:idnum , action:"delete" , filename : x })

    }


}



function cancelButton(x){
    document.getElementById('change_button'+x).style.display = 'block';
    document.getElementById('change_coordinates'+x).style.display = 'none';
}


function submitChanges(x){
    document.getElementById('change_coordinates'+x).style.display = 'none';
    document.getElementById('change_button'+x).style.display = 'block';

    let idnum = document.getElementById(x+'block').getAttribute('idnum')
    let new_coord = document.getElementById('coord_change_text'+x).value

    let req = $.post('update', {idnum:idnum , action:"change" , filename : x , new_coord:new_coord },function(data){ 
            updateFilename(x, data.newName)

     } )
    

}

function  changeButton(x){
    document.getElementById('change_coordinates'+x).style.display = 'block';
    document.getElementById('change_button'+x).style.display = 'none';

}






function updateFilename(oldName, newName){
    document.getElementById(oldName + 'button').onclick = function(){fn1( '/static/' + newName , newName + 'button'  , newName    , '/static/stock.html' )}
    document.getElementById(oldName + 'removebutton').onclick = function(){  fn2(newName) }
    document.getElementById(oldName + 'paragraph').innerHTML =  ' '+newName+' , '+   '/static/'+  newName  +   ' '
    document.getElementById('change_button'+  oldName ).onclick = function(){  changeButton(newName) }
    document.getElementById( 'cancel_button'+   oldName ).onclick = function(){  cancelButton(newName) }
    document.getElementById( 'submit_changes_button'+   oldName ).onclick = function(){  submitChanges(newName) }

    
    document.getElementById(oldName + 'block' ).id = newName +'block';
    document.getElementById(oldName + 'button' ).id = newName +'button';
    document.getElementById(oldName  ).id = newName ;
    document.getElementById(oldName + 'paragraph' ).id = newName +'paragraph';
    document.getElementById( 'change_button' +  oldName  ).id = 'change_button' + newName ;
    document.getElementById( 'change_coordinates' +  oldName  ).id = 'change_coordinates' + newName ;
    document.getElementById( 'coord_change_text' +  oldName  ).id = 'coord_change_text' + newName ;
    document.getElementById(oldName + 'removebutton').id = newName + 'removebutton'
    document.getElementById( 'cancel_button' + oldName ).id = 'cancel_button' + newName 
    document.getElementById( 'submit_changes_button' + oldName ).id = 'submit_changes_button' + newName 
    document.getElementById(newName + 'paragraph').innerHTML =  ' '+newName+' , '+   '/static/'+  newName  +   ' '
    $('#'+newName + 'paragraph').html(' '+newName+' , '+   '/static/'+  newName  +   ' ')

    if ( document.getElementById(newName+'button').innerHTML == 'show' ){
        document.getElementById(newName).src = '/static/'+newName
    }


}



//onclick="fn1( '{{ url_for('static', filename=name.filename)   }}' , '{{name.filename + 'button' }}' , '{{name.filename}}'    , '{{ url_for('static', filename= 'stock.html' )   }}'     ) "

