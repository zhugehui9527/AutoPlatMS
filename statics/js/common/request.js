/**
 * Created by zhanghui559 on 2017/11/6.
 */

function addRequestParams() {
    var length = $("urlParameter .row-param").length;
    var addNum = length;
    var paramHtml = "<div class='row-param'>"
        + "<input type='text' style='display:none;' value='0' name=\"urlParameter["
        + addNum
        + "].id\">"
        + "<input type='text'  class='variable-input paramKey' placeholder='参数名'  name=\"urlParameter["
        + addNum
        + "].paramKey\">"
        + "<input type='text' class='variable-input defaultValue' placeholder='默认值'  name=\"urlParameter["
        + addNum
        + "].defaultValue\">"
        + "<button class='btn btn-box-tool' onclick='removeRequestParams(this);' ><i class='fa fa-times'></i></button> "
        + "<a class='btn btn-box-tool' onclick='addRequestParams();' ><i class='fa fa-plus'></i></a> "
        + "</div>";
    $("#urlParameter").append(paramHtml);

}

function removeRequestParams(obj) {
    var removeobj = $(obj).parent();
    removeobj.remove();
    
}

