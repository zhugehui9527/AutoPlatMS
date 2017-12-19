/**
 * Created by zhanghui559 on 2017/11/20.
 */
    // 分页
    //提示信息
        var lang = {
            "sProcessing": "处理中...",
            "sLengthMenu": "每页 _MENU_ 项",
            "sZeroRecords": "没有匹配结果",
            "sInfo": "当前显示第 _START_ 至 _END_ 项，共 _TOTAL_ 项。",
            "sInfoEmpty": "当前显示第 0 至 0 项，共 0 项",
            "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
            "sInfoPostFix": "",
            "sSearch": "搜索:",
            "sUrl": "",
            "sEmptyTable": "表中数据为空",
            "sLoadingRecords": "载入中...",
            "sInfoThousands": ",",
            "oPaginate": {
                "sFirst": "首页",
                "sPrevious": "上页",
                "sNext": "下页",
                "sLast": "末页",
                "sJump": "跳转",

            },
            "oAria": {
                "sSortAscending": ": 以升序排列此列",
                "sSortDescending": ": 以降序排列此列"
            }
        };

  // $(function () {

    $('#dataform').DataTable({
      "paging": true,
      "lengthChange": true,
      "searching": false, //禁用原生搜索
      "ordering": true,
      "info": true,
        bStateSave:true, //刷新dataTable后会仍然保留在当前页
//"autoWidth": true, //禁用自动调整列宽
//processing: true,  //隐藏加载提示,自行处理
       language: lang,  //提示信息
//stripeClasses: ["odd", "even"],  //为奇偶行加上样式，兼容不支持CSS伪类的场合
//orderMulti: false,  //启用多列排序
       order: [],  //取消默认排序查询,否则复选框一列会出现小箭头
//renderer: "bootstrap",  //渲染样式：Bootstrap和jquery-ui

       columnDefs: [{
                "targets": 'nosort',  //列的样式名
                "orderable": false    //包含上样式名‘nosort’的禁止排序
            }]

    });
  // }).();


$("div.dataTables_paginate").css("text-align","left");
