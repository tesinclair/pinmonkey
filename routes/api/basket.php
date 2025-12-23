<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::post('/add', function(){
    return response()->json([
        'message' => 'not implemented'
    ], 501);
});

Route::delete('/remove', function(){
    return response()->json([
        'message' => 'not implemented'
    ], 501);
});

Route::put('/edit', function(){
    return response()->json([
        'message' => 'not implemented'
    ], 501);
});

Route::get('/', function(){
    return response()->json([
        'message' => 'not implemented'
    ], 501);
});

