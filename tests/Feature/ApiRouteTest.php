<?php

test('the api returns 200 for status route', function() {
    $res = $this->get('/api/status');
    $res->assertStatus(200);
});

test('the api returns not implemented response', function ($endpoint, $method) {
    $res = $this->$method($endpoint);
    $res->assertStatus(501);
})->with([
    ["/api/admin/logout", "get"],
    ["/api/admin/login", "get"],
    ["/api/basket", "get"],
    ["/api/checkout/create-session", "get"],
    ["/api/shop", "get"],
    ["/api/admin/add-item", "post"],
    ["/api/basket/add", "post"],
    ["/api/admin/update-item", "put"],
    ["/api/basket/edit", "put"],
    ["/api/checkout/update-stock", "put"],
    ["/api/admin/delete-item", "delete"],
    ["/api/basket/remove", "delete"]
]);

