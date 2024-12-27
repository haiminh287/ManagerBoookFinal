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
        method:"patch",
        body: JSON.stringify({
            reason_state: "CLIENTREQUIRED"
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        let item = document.getElementById(`item_${cancel_order_id}`);
        // console.log('have get');
        // console.log(`item_${cancel_order_id}`)
        item.style.display = 'none';
    })
}

function confirmOrder(order_id) {
    fetch(`/api/orders/${order_id}`, {
        method:"patch"
    }).then(res => res.json()).then(data => {
        let item = document.getElementById(`item_${order_id}`);
        item.style.display='none';
    })
}