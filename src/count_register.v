module count_register (
    input wire capture, advance, clk, rst_n,
    input wire [4:0] count,
    output reg [4:0] active
);
    reg [4:0] stored;

    always @(posedge clk) begin
        if (~rst_n) begin
            active <= 0;
            stored <= 0;
        end
        else begin
            if (capture) begin
                stored <= count;
            end
            if (advance) begin
                active <= stored;
                stored <= 0;
            end
        end
    end

endmodule