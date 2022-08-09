$(document).ready(function () {
    let t_body = ""
    let t_head = "<tr>"
    
    $.ajax({
        type: 'get',
        url: 'ajax/get_urls/',

        success: function (data) {
            let arr = eval(data)
            for (let i=0; i < arr.length; i++){
                let fields = arr[i]['fields']

                console.log(Object.entries(fields)[0]['url'])
                
                
                // #103d10
                // #660000
                // #625f5e
                // style="background-color: #103d10; color: white"
                let t_body_helper = ""
                let style = ""
                for (const [key, value] of Object.entries(fields)) {
                    // create table heading
                    if(i === 0 & key !== 'status' ){
                        t_head += `<th>${key}</th>`
                    }
                    // create table heading ends

                    if (key === 'status'){
                        if(value === '1'){
                            style += `"background-color: #103d10; color: white;"`
                        }else if(value === '0'){
                            style += `"background-color: #660000; color: white;"`
                        }else{
                            style += `"background-color: #625f5e; color: white;"`
                        }
                        continue
                    }
                    if( key === 'url'){
                        t_body_helper += `<td><a href="${value}">${value.slice(0, 70)}...</a></td>`
                    }else if(key === 'created_date' || key === 'last_checked'){
                        t_body_helper += `<td>${new Date(value).toLocaleString("en-US", {hourCycle: 'h23'})}</td>`
                    }else{
                        t_body_helper += `<td>${value}</td>`
                    }
                }
                t_head += "</tr>"
                t_body += `<tr style=${style}>${t_body_helper}</tr>`
                
            }
            let final_table = `
            <thead>${t_head}</thead>
            <tfoot>${t_head}</tfoot>
            <tbody>${t_body}</tbody>
            `
            $('#urls_table').append(final_table)
        },
        error: function (error) {
            $('#urls_table').append("<h1>Something went wrong!</h1>")
        }
    })
});