const vue = new Vue({
    el: '#app',
    delimiters: ['[[',']]'],
    data: {
        BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        // BASE_URL: 'http://localhost:8000/',
        name: null,
        req_msg: '',
        email: 'tempovola@gmail.com',
        phone: '76983',
    },
    methods: {
        getCookie: function (name) {
            if (!document.cookie) {
                return null;
            }

            const xsrfCookies = document.cookie.split(';')
                .map(c => c.trim())
                .filter(c => c.startsWith(name + '='));

            if (xsrfCookies.length === 0) {
                return null;
            }

            return decodeURIComponent(xsrfCookies[0].split('=')[1]);
        },

        redirect_to_shop: function() {
            window.location.assign(this.BASE_URL + 'customer/shop');
        },

        logout: function() {
            axios({
                method: 'get',
                url: this.BASE_URL + 'customer/logout/',
            }).then(response =>{
                if (response.status === 200) {
                    window.location.replace(this.BASE_URL)
                }else {
                    this.$bvToast.show('req');
                    this.req_msg = 'خروج در حال حاضر ممکن نیست.'
                }
            })
                .catch(response => {
                    this.$bvToast.show('req');
                    this.req_msg = 'خروج در حال حاضر ممکن نیست.'
                })
        }
    },
    created(){
        document.querySelector('div').classList.remove('hid');
    }
});
