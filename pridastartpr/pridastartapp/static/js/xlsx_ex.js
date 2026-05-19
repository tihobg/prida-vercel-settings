function myFunc(type)
{
    var data = document.getElementById('table1');
    var file = XLSX.utils.table_to_book(data, sheet{sheet: "sheet1"});
    XLSX.write(file, {bookType: type, bookSST: true, type: base64})
    XLSX.writeFile(file, 'file.' + type)
    const button = document.getElementById("export_button2");
    button.addEventListener('click', () => {html_table_to_excel('xlsx')};
    button.onClick = () => alert("You clicked me!")
    alert("Hello");
}
//

//function html_table_to_excel(type)
//    {
//        var data = document.getElementById('table1');
//        var file = XLSX.utils.table_to_book(data, sheet{sheet: "sheet1"});
//        XLSX.write(file, {bookType: type, bookSST: true, type: base64})
//        XLSX.writeFile(file, 'file.' + type)
//
//    }
//    const export_button = document.getElementById('export_button2');
//    export_button.addEventListener('click', () => {
//        html_table_to_excel('xlsx');
//    });