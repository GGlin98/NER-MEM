function postData() {
    text = document.getElementById("text").value;
    const clf = $('#clf option:selected').text()

    $.ajax({
        url: 'index.html',
        type: 'post',
        data: JSON.stringify({
            "text": text,
            "clf": clf
        }),
        contentType: 'application/json',
        dataType: 'json',
        success: successGetJson
    });
}

function successGetJson(data) {
    // $('#choose_clf').hide();

    const text_form = document.getElementById("text_form");

    document.body.style.backgroundColor = "#fff";

    data = eval(data);

    const p_content = document.createElement('P');
    p_content.id = 'p_content';

    for (let i = 0; i < data.length; i++) {
        let s;
        if (data[i]['result'] === 'PERSON') {
            s = document.createElement('span');
            s.className = 'PERSON';
        } else {
            s = document.createElement('span');
            s.className = 'O';
        }
        if (data[i]['prob'] !== undefined)
            s.setAttribute('title', data[i]['word'] + '\nP(PERSON) = ' + data[i]['prob'].toFixed(4) + '\nP(O) = ' + (1 - data[i]['prob']).toFixed(4));
        s.innerHTML = data[i]['word'] + ' ';
        p_content.appendChild(s);
    }
    text_form.parentNode.insertBefore(p_content, text_form.nextSibling)
    text_form.style.display = 'none';

    let btn_back = document.getElementById('btn_back');
    if (btn_back != null) {
        btn_back.style.display = 'block';
    } else {
        btn_back = document.createElement('input');
        const header = document.getElementById('header');

        btn_back.type = 'button';
        btn_back.setAttribute('id', 'btn_back');
        btn_back.value = 'Back';
        header.appendChild(btn_back);
        btn_back.addEventListener('click', goBack);
    }
}

function goBack() {
    const btn_back = document.getElementById('btn_back');
    const p_content = document.getElementById('p_content');
    const text_form = document.getElementById("text_form");

    // $('#choose_clf').show();

    document.body.style.backgroundColor = "#f0f0f0";
    btn_back.style.display = 'none';
    p_content.remove()
    text_form.style.display = 'block';
}

function changeModel() {
    let btn_back = document.getElementById('btn_back');
    if (btn_back == null || btn_back.style.display === 'none') {
    } else {
        const p_content = document.getElementById('p_content');
        p_content.remove()
        postData();
    }
}

$(function () {
    $("#clf").selectmenu();
});

let text;
const btn_submit = document.getElementById('text_submit');
btn_submit.addEventListener('click', postData);
$('#clf').on('selectmenuchange', changeModel)
