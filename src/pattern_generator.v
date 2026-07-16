module pattern_generator (
    input wire video_active,
    input wire [9:0] x_pos,
    output reg [1:0] red, green, blue
);

    always @(*) begin
        if (video_active) begin
            red = {2{x_pos[7]}};
            green = {2{x_pos[6]}};
            blue = {2{x_pos[5]}};
        end
        else begin
            red = 2'b00;
            green = 2'b00;
            blue = 2'b00;
        end
    end

endmodule