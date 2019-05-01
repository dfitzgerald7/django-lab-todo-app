

window.onload = () => {
    let num = 0
    const el = document.getElementById('todo_button')
    if (el){
        el.addEventListener('click', event => {
            document.getElementById('todo_form_div').append('<p> a todo </a>')
            num += 1
            console.log(num)
        })
    }


    //code from 
    //https://stackoverflow.com/questions/501719/dynamically-adding-a-form-to-a-django-formset-with-ajax
    $('#add_more').click(function() {
        var form_idx = $('#id_form-TOTAL_FORMS').val();
        $('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
        $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });
}