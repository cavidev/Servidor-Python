/**
 * Created by Carlos Mario on 4/9/2016.
 */

var $ = jQuery;

$(function()
{
    var submit_form;
    submit_form = function (e) {
        $.getJSON('/_add_numbers', {
            a: $('input[name="a"]').val(),
            b: $('input[name="b"]').val()
        }, function (data) {
            $('#result').text(data.result);
            $('input[name=a]').focus().select();
        });
        return false;
    };

//Lee el evento del click del elemento.
$("a#calculate").bind('click', submit_form);
//Lee el evento de la tecla enter.
$('input[type=text]').bind('keydown', function(e) {
    if (e.keyCode != 13) {
    } else submit_form(e);
});

$('input[name=a]').focus();
});
