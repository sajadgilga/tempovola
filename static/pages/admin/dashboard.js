const vue = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        BASE_URL: ' https://tempovolaapp.herokuapp.com/',
        // BASE_URL: 'http://localhost:8000/',
        req_msg: '',
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

        logout: function() {
            axios({
                method: 'get',
                url: this.BASE_URL + 'admin/logout/'
            }).then(response => window.location.replace = this.BASE_URL + 'admin/')
                .catch(response => this.show_alert('مشکل در خروج بوجود آمده. لطفا دوباره تلاش کنید'))
        },

        enter_order_list: function() {
            window.location.href =this.BASE_URL + 'admin/order_list';
        },

        enter_profile_making: function() {
            window.location.assign(this.BASE_URL + 'admin/profile_maker');
        },

        enter_product_making: function() {
            window.location.assign(this.BASE_URL + 'admin/product_maker');
        },

        get_order_excel: function() {
            axios({
                method: 'get',
                url: this.BASE_URL + 'admin/order_excl',
                responseType: 'blob', // important
            }).then((response) => {
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', 'سفارشات.xls'); //or any other extension
                document.body.appendChild(link);
                link.click();
            })
                .catch(response => this.show_alert('مشکلی در دریافت فایل بوجود آمده. دوباره تلاش کنید'));
        },

        show_alert(msg){
            this.req_msg = msg;
            this.$bvToast.show('req');
        },
    }
});