<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/status', function(){
    return ["status" => 200];
});

Route::prefix('shop')
    ->group(base_path('routes/api/shop.php'));

Route::prefix('admin')
    ->group(base_path('routes/api/admin.php'));

Route::prefix('basket')
    ->group(base_path('routes/api/basket.php'));

Route::prefix('checkout')
    ->group(base_path('routes/api/checkout.php'));
