# -*- coding:utf-8 -*-
from django.http import HttpResponse


def report_template(request):

    report_html = '''
        <!DOCTYPE html>
            <html>
              <head>
                <meta charset="utf-8"/>
                <title>Test Report</title>
                <style>body {
                font-family: Helvetica, Arial, sans-serif;
                font-size: 12px;
                min-width: 1200px;
                color: #999;
            }
            h2 {
                font-size: 16px;
                color: black;
            }

            p {
                color: black;
            }

            a {
                color: #999;
            }

            table {
                border-collapse: collapse;
            }

            /******************************
             * SUMMARY INFORMATION
             ******************************/

            #environment td {
                padding: 5px;
                border: 1px solid #E6E6E6;
            }

            #environment tr:nth-child(odd) {
                background-color: #f6f6f6;
            }

            /******************************
             * TEST RESULT COLORS
             ******************************/
            span.passed, .passed .col-result {
                color: green;
            }
            span.skipped, span.xfailed, span.rerun, .skipped .col-result, .xfailed .col-result, .rerun .col-result {
                color: orange;
            }
            span.error, span.failed, span.xpassed, .error .col-result, .failed .col-result, .xpassed .col-result  {
                color: red;
            }


            /******************************
             * RESULTS TABLE
             *
             * 1. Table Layout
             * 2. Extra
             * 3. Sorting items
             *
             ******************************/

            /*------------------
             * 1. Table Layout
             *------------------*/

            #results-table {
                border: 1px solid #e6e6e6;
                color: #999;
                font-size: 12px;
                width: 100%
            }

            #results-table th, #results-table td {
                padding: 5px;
                border: 1px solid #E6E6E6;
                text-align: left
            }
            #results-table th {
                font-weight: bold
            }

            /*------------------
             * 2. Extra
             *------------------*/

            .log:only-child {
                height: inherit
            }
            .log {
                background-color: #e6e6e6;
                border: 1px solid #e6e6e6;
                color: black;
                display: block;
                font-family: "Courier New", Courier, monospace;
                height: 230px;
                overflow-y: scroll;
                padding: 5px;
                white-space: pre-wrap
            }
            div.image {
                border: 1px solid #e6e6e6;
                float: right;
                height: 240px;
                margin-left: 5px;
                overflow: hidden;
                width: 320px
            }
            div.image img {
                width: 320px
            }
            .collapsed {
                display: none;
            }
            .expander::after {
                content: " (show details)";
                color: #BBB;
                font-style: italic;
                cursor: pointer;
            }
            .collapser::after {
                content: " (hide details)";
                color: #BBB;
                font-style: italic;
                cursor: pointer;
            }

            /*------------------
             * 3. Sorting items
             *------------------*/
            .sortable {
                cursor: pointer;
            }

            .sort-icon {
                font-size: 0px;
                float: left;
                margin-right: 5px;
                margin-top: 5px;
                /*triangle*/
                width: 0;
                height: 0;
                border-left: 8px solid transparent;
                border-right: 8px solid transparent;
            }

            .inactive .sort-icon {
                /*finish triangle*/
                border-top: 8px solid #E6E6E6;
            }

            .asc.active .sort-icon {
                /*finish triangle*/
                border-bottom: 8px solid #999;
            }

            .desc.active .sort-icon {
                /*finish triangle*/
                border-top: 8px solid #999;
            }
            </style></head>
              <body onLoad="init()">
                <script>/* This Source Code Form is subject to the terms of the Mozilla Public
             * License, v. 2.0. If a copy of the MPL was not distributed with this file,
             * You can obtain one at http://mozilla.org/MPL/2.0/. */


            function toArray(iter) {
                if (iter === null) {
                    return null;
                }
                return Array.prototype.slice.call(iter);
            }

            function find(selector, elem) {
                if (!elem) {
                    elem = document;
                }
                return elem.querySelector(selector);
            }

            function find_all(selector, elem) {
                if (!elem) {
                    elem = document;
                }
                return toArray(elem.querySelectorAll(selector));
            }

            function sort_column(elem) {
                toggle_sort_states(elem);
                var colIndex = toArray(elem.parentNode.childNodes).indexOf(elem);
                var key;
                if (elem.classList.contains('numeric')) {
                    key = key_num;
                } else if (elem.classList.contains('result')) {
                    key = key_result;
                } else {
                    key = key_alpha;
                }
                sort_table(elem, key(colIndex));
            }

            function show_all_extras() {
                find_all('.col-result').forEach(show_extras);
            }

            function hide_all_extras() {
                find_all('.col-result').forEach(hide_extras);
            }

            function show_extras(colresult_elem) {
                var extras = colresult_elem.parentNode.nextElementSibling;
                var expandcollapse = colresult_elem.firstElementChild;
                extras.classList.remove("collapsed");
                expandcollapse.classList.remove("expander");
                expandcollapse.classList.add("collapser");
            }

            function hide_extras(colresult_elem) {
                var extras = colresult_elem.parentNode.nextElementSibling;
                var expandcollapse = colresult_elem.firstElementChild;
                extras.classList.add("collapsed");
                expandcollapse.classList.remove("collapser");
                expandcollapse.classList.add("expander");
            }

            function show_filters() {
                var filter_items = document.getElementsByClassName('filter');
                for (var i = 0; i < filter_items.length; i++)
                    filter_items[i].hidden = false;
            }

            function add_collapse() {
                // Add links for show/hide all
                var resulttable = find('table#results-table');
                var showhideall = document.createElement("p");
                showhideall.innerHTML = '<a href="javascript:show_all_extras()">Show all details</a> / ' +
                                        '<a href="javascript:hide_all_extras()">Hide all details</a>';
                resulttable.parentElement.insertBefore(showhideall, resulttable);

                // Add show/hide link to each result
                find_all('.col-result').forEach(function(elem) {
                    var extras = elem.parentNode.nextElementSibling;
                    var expandcollapse = document.createElement("span");
                    if (elem.innerHTML === 'Passed') {
                        extras.classList.add("collapsed");
                        expandcollapse.classList.add("expander");
                    } else {
                        expandcollapse.classList.add("collapser");
                    }
                    elem.appendChild(expandcollapse);

                    elem.addEventListener("click", function(event) {
                        if (event.currentTarget.parentNode.nextElementSibling.classList.contains("collapsed")) {
                            show_extras(event.currentTarget);
                        } else {
                            hide_extras(event.currentTarget);
                        }
                    });
                })
            }

            function init () {
                reset_sort_headers();

                add_collapse();

                show_filters();

                toggle_sort_states(find('.initial-sort'));

                find_all('.sortable').forEach(function(elem) {
                    elem.addEventListener("click",
                                          function(event) {
                                              sort_column(elem);
                                          }, false)
                });

            };

            function sort_table(clicked, key_func) {
                var rows = find_all('.results-table-row');
                var reversed = !clicked.classList.contains('asc');
                var sorted_rows = sort(rows, key_func, reversed);
                /* Whole table is removed here because browsers acts much slower
                 * when appending existing elements.
                 */
                var thead = document.getElementById("results-table-head");
                document.getElementById('results-table').remove();
                var parent = document.createElement("table");
                parent.id = "results-table";
                parent.appendChild(thead);
                sorted_rows.forEach(function(elem) {
                    parent.appendChild(elem);
                });
                document.getElementsByTagName("BODY")[0].appendChild(parent);
            }

            function sort(items, key_func, reversed) {
                var sort_array = items.map(function(item, i) {
                    return [key_func(item), i];
                });
                var multiplier = reversed ? -1 : 1;

                sort_array.sort(function(a, b) {
                    var key_a = a[0];
                    var key_b = b[0];
                    return multiplier * (key_a >= key_b ? 1 : -1);
                });

                return sort_array.map(function(item) {
                    var index = item[1];
                    return items[index];
                });
            }

            function key_alpha(col_index) {
                return function(elem) {
                    return elem.childNodes[1].childNodes[col_index].firstChild.data.toLowerCase();
                };
            }

            function key_num(col_index) {
                return function(elem) {
                    return parseFloat(elem.childNodes[1].childNodes[col_index].firstChild.data);
                };
            }

            function key_result(col_index) {
                return function(elem) {
                    var strings = ['Error', 'Failed', 'Rerun', 'XFailed', 'XPassed',
                                   'Skipped', 'Passed'];
                    return strings.indexOf(elem.childNodes[1].childNodes[col_index].firstChild.data);
                };
            }

            function reset_sort_headers() {
                find_all('.sort-icon').forEach(function(elem) {
                    elem.parentNode.removeChild(elem);
                });
                find_all('.sortable').forEach(function(elem) {
                    var icon = document.createElement("div");
                    icon.className = "sort-icon";
                    icon.textContent = "vvv";
                    elem.insertBefore(icon, elem.firstChild);
                    elem.classList.remove("desc", "active");
                    elem.classList.add("asc", "inactive");
                });
            }

            function toggle_sort_states(elem) {
                //if active, toggle between asc and desc
                if (elem.classList.contains('active')) {
                    elem.classList.toggle('asc');
                    elem.classList.toggle('desc');
                }

                //if inactive, reset all other functions and add ascending active
                if (elem.classList.contains('inactive')) {
                    reset_sort_headers();
                    elem.classList.remove('inactive');
                    elem.classList.add('active');
                }
            }

            function is_all_rows_hidden(value) {
              return value.hidden == false;
            }

            function filter_table(elem) {
                var outcome_att = "data-test-result";
                var outcome = elem.getAttribute(outcome_att);
                class_outcome = outcome + " results-table-row";
                var outcome_rows = document.getElementsByClassName(class_outcome);

                for(var i = 0; i < outcome_rows.length; i++){
                    outcome_rows[i].hidden = !elem.checked;
                }

                var rows = find_all('.results-table-row').filter(is_all_rows_hidden);
                var all_rows_hidden = rows.length == 0 ? true : false;
                var not_found_message = document.getElementById("not-found-message");
                not_found_message.hidden = !all_rows_hidden;
            }
            </script>
                <p>Report generated on {{ generate_time }} by<a href="http://127.0.0.1:8000/casemanage/group/result/"> ATMS</a>  V1.0.1</p>
                <h2>Environment</h2>
                <table id="environment">

                <tr>
                    <td>Platform Version</td>
                    <td>Python Version</td>
                    <td>Django Version</td>
                    <td>Celery Version</td>
            {#        <td>JAVA_HOME</td>#}
                  </tr>
                  <tr>
                    <td>{{ platform }}</td>
                      <td>{{ python_version }}</td>
                      <td>{{ django_version }}</td>
                      <td>{{ celery_version }}</td>
            {#          <td>{{ java_home }}</td>#}
                  </tr>

                </table>

                <h2>Build </h2>
                <table id="environment">

                <tr>
                    <td>构建ID</td>
                    <td>任务名称</td>
                    <td>构建名称</td>
                    <td>任务状态</td>
                    <td>任务耗时</td>
                    <td>完成时间</td>
                    <td>任务参数</td>
                  </tr>
                  <tr>
                    <td>{{ build_id }}</td>
                      <td>{{ get_job_name }}</td>
                      <td>{{ name }}</td>
                      <td>{{ state }}</td>
                      <td>{{ runtime |floatformat:3}}</td>
                      <td>{{ tstamp |date:"Y-m-d H:i:s"}}</td>
                      <td>{{ args }}</td>
                  </tr>

                </table>
                <h2>Summary</h2>
                <p>{{ summary.res_count }} tests ran in {{ summary.res_duration }} seconds. </p>
                <p class="filter" hidden="true">(Un)check the boxes to filter the results.</p>
                <input checked="true" class="filter" data-test-result="passed" hidden="true" name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/>
                <span class="passed">{{ summary.res_success }} passed</span>,
                <input checked="true" class="filter" data-test-result="failed" disabled="true" hidden="true" name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/>
                <span class="failed">{{ summary.res_fail }} failed</span>, <input checked="true" class="filter" data-test-result="error" disabled="true" hidden="true" name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/>
                <span class="error">{{ summary.res_error }} errors</span>, <input checked="true" class="filter" data-test-result="xfailed" hidden="true" name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/>
                <span class="rerun">{{ summary.res_rerun }} rerun</span>
                <h2>Results</h2>
                <table id="results-table">
                  <thead id="results-table-head">
                    <tr>
                      <th class="sortable result initial-sort" col="result">结果</th>
                      <th class="sortable" col="name">接口名称</th>
                      <th class="sortable numeric" col="duration">耗时</th>
                        <th>请求方法</th>
                      <th>请求路径</th>
                    </tr>
                    <tr hidden="true" id="not-found-message">
                      <th colspan="6">No results found. Try to check the filters</th></tr></thead>

                    {% for c in cases %}
                        {% ifequal c.status 2 %}
                            <tbody class="passed results-table-row">
                            <tr>
                              <td class="col-result">成功</td>
                            <td class="col-name">{{ c.case_name }}</td>
                              <td class="col-duration">{{ c.duration }}</td>
                                {% ifequal c.request_method 1 %}
                                    <td class="col-links">GET</td>
                                    {% endifequal %}
                                {% ifequal c.request_method 2 %}
                                    <td class="col-links">POST</td>
                                    {% endifequal %}
                              <td class="col-links">{{ c.path }}</td>
                                 <tr class="collapsed">
                                    <td class="extra" colspan="6">
                                        <div class="empty log">{{ c.traceback }}</div>
                                    </td>
                                </tr>
                            </tr>
                            </tbody>
                        {% endifequal %}

                         {% ifequal c.status 3 %}
                            <tbody class="failed results-table-row">
                            <tr>
                              <td class="col-result">失败</td>
                            <td class="col-name">{{ c.case_name }}</td>
                              <td class="col-duration">{{ c.duration }}</td>
                                {% ifequal c.request_method 1 %}
                                    <td class="col-links">GET</td>
                                    {% endifequal %}
                                {% ifequal c.request_method 2 %}
                                    <td class="col-links">POST</td>
                                    {% endifequal %}

                              <td class="col-links">{{ c.path }}</td>
                            </tr>
                            <tr class="extra">
                                    <td class="extra" colspan="6">
                                        <div class="empty log">{{ c.traceback }}</div>
                                    </td>
                                </tr>
                             </tbody>
                        {% endifequal %}

                        {% ifequal c.status 4 %}
                            <tbody class="error results-table-row">
                            <tr>
                              <td class="col-result">错误</td>
                            <td class="col-name">{{ c.case_name }}</td>
                              <td class="col-duration">{{ c.duration }}</td>
                                {% ifequal c.request_method 1 %}
                                    <td class="col-links">GET</td>
                                    {% endifequal %}
                                {% ifequal c.request_method 2 %}
                                    <td class="col-links">POST</td>
                                    {% endifequal %}
                              <td class="col-links">{{ c.path }}</td>
                            </tr>
                            <tr class="extra">
                                    <td class="extra" colspan="6">
                                        <div class="empty log">{{ c.traceback }}</div>
                                    </td>
                                </tr>
                            </tbody>
                        {% endifequal %}

                    {% endfor %}

                  </table>
              </body>
            </html>
            '''
    return report_html