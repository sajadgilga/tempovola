const vue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        // BASE_URL: 'http://localhost:8000/',
        req_msg: '',
        alert_header: ' ورود ناموفقیت آمیز',
        orders: [],
    },
    methods: {
        returnToPanel: function(){
            window.location.href = this.BASE_URL + 'admin/dashboard'
        },

        show_alert(msg){
            this.req_msg = msg;
            this.$bvToast.show('req');
        },
    },
    created(){
        axios({
            method: 'get',
            url: this.BASE_URL + 'admin/fetch_orders',
            headers: {
                'Accept': 'Application/json',
                'Content_Type': 'Application/json'
            }
        }).then(respond => {


            document.querySelector('div').classList.remove('hid');
        }).catch(respond => {

        })
    }
});
