module coordinate_mapper (
    input wire [9:0] x_pos, y_pos,
    output wire signed [17:0] c_x, c_y
);
    wire signed [28:0] x_product, y_product;

    assign x_product = ($signed({1'b0, x_pos}) * 18'sd179);
    assign y_product = ($signed({1'b0, y_pos}) * 18'sd137);

    assign c_x = x_product[17:0] + (-18'sd81920);
    assign c_y = y_product[17:0] + (-18'sd32768);

endmodule