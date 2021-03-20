   var map_myChart = echarts.init(document.querySelector(".map .chart"));
    // 2. 指定配置和数据
    // 2. 指定配置和数据
    var map_data = [
        { name: "河北", value: 900 }
    ];
    var map_option = {
        tooltip: {
            triggerOn: "click",
            formatter: function(e, t, n) {
                return '.5' == e.value ? e.name + "：有疑似病例" : e.seriesName + "<br />" + e.name + "：" + e.value
            }
        },
        toolbox: { //右边那三个图标
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
                dataView: { readOnly: false, title: 'hello', textColor: "#777" },
                restore: {},
                saveAsImage: {}
            }
        }, // 提供下载工具
        visualMap: { //左边的图标
            min: 0,
            max: 100000,
            left: 26,
            bottom: 30,
            showLabel: !0,
            text: ["高", "低"],
            textStyle: {
                fontSize: 12,
                color: "#fff"
            },
            pieces: [{
                gt: 10000,
                label: "> 10000人",
                color: "#7f1100"
            }, {
                gte: 1000,
                lte: 10000,
                label: "1000 - 10000人",
                color: "#ff5428"
            }, {
                gte: 100,
                lt: 1000,
                label: "100 - 1000人",
                color: "#ff8c71"
            }, {
                gt: 0,
                lt: 100,
                label: "1 - 100人",
                color: "#ffd768"
            }, {
                value: 0,
                color: "#ffffff"
            }],
            show: !0
        },
        grid: [{
                right: '5%',
                top: '20%',
                bottom: '10%',
                width: '20%'
            },

        ],

        geo: {
            map: "china",
            // right:'25%',
            // left:'18%',
            center: [105.97, 30.71],
            roam: true,
            scaleLimit: { //通过鼠标控制的缩放
                min: 1,
                max: 2
            },
            zoom: 1.1, //当前缩放比例
            top: 120, //组件离容器上方的距离
            label: {
                normal: {
                    show: !0,
                    fontSize: "14",
                    color: "#fff"
                }
            },
            //         regions: [{
            //     name: '青海',
            //     label: {
            //         normal: {

            //         }
            //     }
            // }],
            itemStyle: {
                normal: {
                    //shadowBlur: 50,
                    //shadowColor: 'rgba(0, 0, 0, 0.2)',
                    borderColor: "rgba(0, 0, 0, 0.5)"
                },
                emphasis: {
                    areaColor: "#f2d5ad", //鼠标放上去的颜色
                    shadowOffsetX: 0,
                    shadowOffsetY: 0,
                    borderWidth: 0
                }
            }
        },
        series: [{
                name: "确诊病例",
                type: "map",
                geoIndex: 0,
                data: map_data
            }]
            // },
            // {
            //         name: '哈喽喽',
            //         type: 'scatter',
            //         itemStyle: itemStyle,
            //         data: window.dataList
            //     }
            // ]
    };
    map_myChart.setOption(map_option);
    window.addEventListener("resize", function() {
        map_myChart.resize();
    });