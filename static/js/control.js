        function get_c1_data(){
            $.ajax({
                url:"/c1",
                success:function(data){
                    $("#main_confirm").text(data.confirm);
                    $("#main_dead").text(data.dead);
                    $("#main_heal").text(data.heal);
                    $("#main_now").text(data.confirm-data.dead-data.heal);
                },
                error:function (xhr,type,errorThrown){

                }
            })
        }
        function get_c2_data() {
            $.ajax({
                url: "/c2",
                success: function (data) {
                    map_option.series[0].data = data.data;
                    map_myChart.setOption(map_option);
                },
                error: function (xhr, type, errorThrown) {
                }
            })
        }
        get_c1_data()
        get_c2_data()