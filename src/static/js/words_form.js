var max_input_count = 30
let input_count = 0

var input_container = document.querySelector("#input-container")
var add_lines_btn = document.querySelector("#add-more-lines")
var clear_lines_btn = document.querySelector("#clear-lines-btn")

console.log("running_word_form")

document.addEventListener("DOMContentLoaded", function(){
    console.log("dom_loaded_in_running_form")
    build_input_list(input_container, 10)
    add_lines_btn.addEventListener("click", (e)=>{return handle_add_lines_btn_click(e)})
    // clear_lines_btn.addEventListener("click", (e) => { return handle_clear_lines_btn_click(e)})
})

function build_input_list(){
    input_count = input_container.childElementCount
    for(let i=0; i<10; i++){
        if (input_count <= max_input_count){
            input_count ++
            input_container.appendChild(word_and_definition_input_group(String(input_count)))
        } 
        update_add_lines_btn()
    }
}

function handle_add_lines_btn_click(e){
    e.preventDefault()
    build_input_list(input_container)
}

function update_add_lines_btn(){
    if (input_count >= max_input_count){
        add_lines_btn.disabled = true
        add_lines_btn.innerText = "max words reached"
    } else {
        add_lines_btn.disabled = false
        add_lines_btn.innerText = "add more"
    }
}

// function handle_clear_lines_btn_click(e){
//     e.preventDefault()
//     input_container.innerHTML = ""
//     build_input_list(input_container)
// }

function word_and_definition_input_group(name){
    const container = document.createElement("li")
    container.className = "mb-2"
    container.innerHTML = `
        <input name="word-${name}" type="text" class="form-control" aria-label="word">
    `
    return container
}

// export {
//     add_lines_btn,
//     clear_lines_btn,
//     handle_add_lines_btn_click,
//     handle_clear_lines_btn_click,
//     build_input_list,
// }