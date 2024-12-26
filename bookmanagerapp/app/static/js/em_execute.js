function loadListBase() {
    var data = document.getElementsByClassName('col-actions')
    // actions = [1,2,3];
    var actions = Array.from(data);
    actions.shift();
    console.log(actions);
    if (actions.length >0) {
        let dipHTML = `<a class="btn btn-primary btn-sm">X</a>`;
        for(let a of actions) 
            a.innerHTML = dipHTML;
    }
    // var test = document.getElementById("chao");
    // test.innerHTML = 'hello'
    console.log('success')
}

function confirmPendingCancel(cancel_order_id) {
    fetch(`/api/cancel_orders/${cancel_order_id}`, {
        method:"put",
        body: JSON.stringify({
            reason_state: "CLIENTREQUIRED"
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        let item = document.getElementById(`item${cancel_order_id}`);
        console.log('have get');
        item.style.display = 'none';
    })
}